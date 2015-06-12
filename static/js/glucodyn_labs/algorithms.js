//g is time in minutes from bolus event, idur=insulin duration
//walsh iob curves
function iob(g,idur) {  
  if(g<=0.0) {
    tot=100.0
  } else if (g>=idur*60.0) {
    tot=0.0
  } else {
    if(idur==3) {
      tot=-3.203e-7*Math.pow(g,4)+1.354e-4*Math.pow(g,3)-1.759e-2*Math.pow(g,2)+9.255e-2*g+99.951
    } else if (idur==4) {
      tot=-3.31e-8*Math.pow(g,4)+2.53e-5*Math.pow(g,3)-5.51e-3*Math.pow(g,2)-9.086e-2*g+99.95
    } else if (idur==5) {
      tot=-2.95e-8*Math.pow(g,4)+2.32e-5*Math.pow(g,3)-5.55e-3*Math.pow(g,2)+4.49e-2*g+99.3
    } else if (idur==6) {
      tot=-1.493e-8*Math.pow(g,4)+1.413e-5*Math.pow(g,3)-4.095e-3*Math.pow(g,2)+6.365e-2*g+99.7
    } 
  }          
  return(tot);
}

//simpsons rule to integrate IOB - can include sf and dbdt as functions of tstar later - assume constants for now
//integrating over flux time tstar 
function intIOB(x1,x2,idur,g) {
  var integral;
  var dx;
  var nn=50; //nn needs to be even
  var ii=1;
  
  //initialize with first and last terms of simpson series
  dx=(x2-x1)/nn;
  integral=iob((g-x1),idur)+iob(g-(x1+nn*dx),idur);

  while(ii<nn-2) {
    integral = integral + 4*iob(g-(x1+ii*dx),idur)+2*iob(g-(x1+(ii+1)*dx),idur);
    ii=ii+2;
  }

  integral=integral*dx/3.0;
  return(integral);

}
            
//scheiner gi curves fig 7-8 from Think Like a Pancreas, fit with a triangle shaped absorbtion rate curve
//see basic math pdf on repo for details
//g is time in minutes,gt is carb type
function cob(g,ct) {  
  
  if(g<=0) {
    tot=0.0
  } else if (g>=ct) {
    tot=1.0
  } else if ((g>0)&&(g<=ct/2.0)) {
    tot=2.0/Math.pow(ct,2)*Math.pow(g,2)
  } else 
    tot=-1.0+4.0/ct*(g-Math.pow(g,2)/(2.0*ct))
    return(tot);
}
    
function deltatempBGI(g,dbdt,sensf,idur,t1,t2) {
  return -dbdt*sensf*((t2-t1)-1/100*intIOB(t1,t2,idur,g));
}

function deltaBGC(g,sensf,cratio,camount,ct) {
  return sensf/cratio*camount*cob(g,ct);
}

function deltaBGI(g,bolus,sensf,idur) {
  return -bolus*sensf*(1-iob(g,idur)/100.0);
}

function deltaBG(g,sensf,cratio,camount,ct,bolus,idur) {
  return deltaBGI(g,bolus,sensf,idur)+deltaBGC(g,sensf,cratio,camount,ct);
}

function GlucodynStats(bg) {
  var min=1000;
  var max=0;
  var sum=0;
  //calc average
  for(var ii=0;ii<bg.length;ii++){
    sum=sum+bg[ii];
    //find min and max
    if(bg[ii]<min) {min=bg[ii];}
    if(bg[ii]>max) {max=bg[ii];}
  }

  averagebg=sum/bg.length;

  //calc square of differences
  var dsq=0;
  for (ii=0;ii<bg.length;ii++){
    dsq=dsq+=Math.pow((bg[ii]-averagebg),2);
  }
  //calc sd
  var sd=Math.pow((dsq/bg.length),0.5);
  
  var result = [];
  result[0] = averagebg;        
  result[1] = sd;
  result[2] = min;
  result[3] = max;
  
  $("#stats_avg").text(Math.round(averagebg));
  $("#stats_min").text(Math.round(min));
  $("#stats_max").text(Math.round(max));
  $("#stats_std").text(Math.round(sd));
          
  return result;

} 
  
//user parameters - carb ratio, sensitivity factor, insulin duration      
if ( localStorage["userdata"] ) {
  var userdata = JSON.parse(localStorage["userdata"]);
} else {
  localStorage["userdata"] = JSON.stringify({cratio:0,sensf:0.0,idur:1,bginitial:0,stats:0,simlength:1,inputeffect:1});
  var userdata = JSON.parse(localStorage["userdata"]);
}

var uevent = [];
var uevent_counter = 0;

var simt = userdata.simlength*60; //total simulation time in min from zero

var simtimeadjustrecommendation = 1 // variable to allow user to receive simulation time recommendations ( valid for 1 session )

var n=Math.floor(simt/5); //points in simulation
var dt=simt/n;
var simbgc = [];
var simbgi = [];
var simbg = [];
var predata =[];

for (i=0;i<n;i++) {
   simbgc[i]=0.0;
   simbgi[i]=0.0;
    simbgi[i]=userdata.bginitial;
}

// Max Sim Time
function RecommendedMaxSimTime(set_trigger) {
  
  if ( uevent.length > 0 && simtimeadjustrecommendation == 1 ) {
    
    var userdata = JSON.parse(localStorage["userdata"]);
      
    var maxsimtime=0;
    for (var ii=0;ii<uevent.length;ii++) {
      var etime=0;

      if(uevent[ii].etype=="bolus") {etime=uevent[ii].time+userdata.idur*60;}
      if (uevent[ii].etype=="carb") {etime=uevent[ii].time+uevent[ii].ctype;}
      if(uevent[ii].etype=="tempbasal") {etime=uevent[ii].t2+userdata.idur*60;}
      if (etime>maxsimtime) {maxsimtime=etime;}    
    }
          
    if ( maxsimtime > userdata.simlength*60 ) {

      $("#simtime_adjust_container").removeClass("hidden");
      $("#simtime_recommend_label").text((Math.ceil(maxsimtime/60))*60);          
              
    } else if ( Math.ceil(maxsimtime/60) < userdata.simlength ) {
    
      $("#simtime_adjust_container").removeClass("hidden");
      $("#simtime_recommend_label").text((Math.ceil(maxsimtime/60))*60);          
    
    } else {

      $("#simtime_adjust_container").addClass("hidden");
    
    }
  
    if ( set_trigger == 1 ) {
    
      userdata.simlength = Math.ceil(maxsimtime/60);
    
      localStorage["userdata"] = JSON.stringify({cratio:userdata.cratio,sensf:userdata.sensf,idur:userdata.idur,bginitial:userdata.bginitial,stats:userdata.stats,simlength:userdata.simlength,inputeffect:userdata.inputeffect});
    
      reloadSliders();
      loadRealData();
      reloadGraphData();          
      
    }
    
  } else {
    
    $("#simtime_adjust_container").addClass("hidden");
    
  }

}
