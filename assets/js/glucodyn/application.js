// Some general UI pack related JS
// Extend JS String with repeat method
String.prototype.repeat = function (num) {
  return new Array(Math.round(num) + 1).join(this);
};

(function ($) {

  // Add segments to a slider
  $.fn.addSliderSegments = function () {
    return this.each(function () {
      var $this = $(this),
          option = $this.slider('option'),
          amount = (option.max - option.min)/option.step,
          orientation = option.orientation;
      if ( 'vertical' === orientation ) {
        var output = '', i;
        for (i = 1; i <= amount - 1; i++) {
            output += '<div class="ui-slider-segment" style="top:' + 100 / amount * i + '%;"></div>';
        }
        $this.prepend(output);
      } else {
        var segmentGap = 100 / (amount) + '%';
        var segment = '<div class="ui-slider-segment" style="margin-left: ' + segmentGap + ';"></div>';
        $this.prepend(segment.repeat(amount - 1));
      }
    });
  };

  $(function () {

    // Checkboxes and Radio buttons
    $('[data-toggle="checkbox"]').radiocheck();
    $('[data-toggle="radio"]').radiocheck();

    // Tooltips
    $('[data-toggle=tooltip]').tooltip('show');

    // jQuery UI Sliders
    var $slider = $('#carb_time_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 0,
        max: simt,
        step: 1,
        value: 0,
        orientation: 'horizontal',
        range: false,
        slide: function(event, ui) {
          $("#carb_time_slider_label").text(ui.value);
        }
      }).addSliderSegments();
    }

    var $slider = $('#carb_amount_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 0,
        max: 200,
        step: 0.5,
        value: 0,
        orientation: 'horizontal',
        range: "min",
        slide: function(event, ui) {
          $("#carb_amount_slider_label").text(ui.value);
        }
      }).addSliderSegments();
    }

    $(".carb_type").change(function(){
      
      // On change, update the slider.
      if ( $("input[name='carb_type']:checked").val() == "low" ) {
        
        $("#carb_type_slider_label").text(240);
        $('#carb_type_slider').slider({value: 240});
        
      } else if ( $("input[name='carb_type']:checked").val() == "medium" ) {

        $("#carb_type_slider_label").text(180);
        $('#carb_type_slider').slider({value: 180});
        
      } else if ( $("input[name='carb_type']:checked").val() == "high" ) {
        
        $("#carb_type_slider_label").text(90);
        $('#carb_type_slider').slider({value: 90});
        
      }
            
    });

    var $slider = $('#carb_type_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 0,
        max: 300,
        step: 1,
        value: 0,
        orientation: 'horizontal',
        range: "min",
        slide: function(event, ui) {
          $("#carb_type_slider_label").text(ui.value);
        }
      }).addSliderSegments();
    }

    var $slider = $('#carb_ratio_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 1,
        max: 100,
        step: 0.5,
        value: userdata.cratio,
        orientation: 'horizontal',
        range: false,
        slide: function(event, ui) {
          $("#carb_ratio_slider_label").text(ui.value);

          var userdata = JSON.parse(localStorage["userdata"]);

          userdata.cratio = ui.value
          
          localStorage["userdata"] = JSON.stringify({cratio:userdata.cratio,sensf:userdata.sensf,idur:userdata.idur,bginitial:userdata.bginitial,stats:userdata.stats,simlength:userdata.simlength,inputeffect:userdata.inputeffect});
          
          reloadGraphData();
          
        }
      }).addSliderSegments();
    }

    var $slider = $('#carb_sensitivity_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 1,
        max: 100,
        step: 0.5,
        value: userdata.sensf,
        orientation: 'horizontal',
        range: false,
        slide: function(event, ui) {
          $("#carb_sensitivity_slider_label").text(ui.value);

          var userdata = JSON.parse(localStorage["userdata"]);

          userdata.sensf = ui.value
          
          localStorage["userdata"] = JSON.stringify({cratio:userdata.cratio,sensf:userdata.sensf,idur:userdata.idur,bginitial:userdata.bginitial,stats:userdata.stats,simlength:userdata.simlength,inputeffect:userdata.inputeffect});
          
          reloadGraphData();
          
        }
      }).addSliderSegments();
    }

    var $slider = $('#insulin_duration_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 1,
        max: 6,
        step: 1.0,
        value: userdata.idur,
        orientation: 'horizontal',
        range: false,
        slide: function(event, ui) {
          $("#insulin_duration_slider_label").text(ui.value);

          var userdata = JSON.parse(localStorage["userdata"]);

          userdata.idur = ui.value
          
          localStorage["userdata"] = JSON.stringify({cratio:userdata.cratio,sensf:userdata.sensf,idur:userdata.idur,bginitial:userdata.bginitial,stats:userdata.stats,simlength:userdata.simlength,inputeffect:userdata.inputeffect});
          
          reloadGraphData();
          
        }
      }).addSliderSegments();
    }
          
    var $slider = $('#initial_bg_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 0,
        max: 300,
        step: 10.0,
        value: userdata.bginitial,
        orientation: 'horizontal',
        range: false,
        slide: function(event, ui) {
          $("#initial_bg_slider_label").text(ui.value);

          var userdata = JSON.parse(localStorage["userdata"]);

          userdata.bginitial = ui.value
          
          localStorage["userdata"] = JSON.stringify({cratio:userdata.cratio,sensf:userdata.sensf,idur:userdata.idur,bginitial:userdata.bginitial,stats:userdata.stats,simlength:userdata.simlength,inputeffect:userdata.inputeffect});
          
          reloadGraphData();
          
        }
      }).addSliderSegments();
    }

    var $slider = $('#sim_duration_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 1,
        max: 24,
        step: 1,
        value: userdata.simlength,
        orientation: 'horizontal',
        range: false,
        slide: function(event, ui) {
          $("#sim_duration_slider_label").text(ui.value);

          var userdata = JSON.parse(localStorage["userdata"]);

          userdata.simlength = ui.value
          
          localStorage["userdata"] = JSON.stringify({cratio:userdata.cratio,sensf:userdata.sensf,idur:userdata.idur,bginitial:userdata.bginitial,stats:userdata.stats,simlength:userdata.simlength,inputeffect:userdata.inputeffect});
          
          reloadGraphData();          
        }, 
        change: function() {
          reloadSliders();
        }
      }).addSliderSegments();
    }
    
    var $slider = $('#bolus_time_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 0,
        max: simt,
        step: 1,
        value: 0,
        orientation: 'horizontal',
        range: false,
        slide: function(event, ui) {
          $("#bolus_time_slider_label").text(ui.value);
        }
      }).addSliderSegments();
    }

    var $slider = $('#bolus_amount_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: 0,
        max: 20,
        step: 0.1,
        value: 0,
        orientation: 'horizontal',
        range: "min",
        slide: function(event, ui) {
          $("#bolus_amount_slider_label").text(ui.value);
        }
      }).addSliderSegments();
    }

    var $slider = $('#tempbasal_amount_slider');
    if ($slider.length > 0) {
      $slider.slider({
        min: -0.2,
        max: 0.2,
        step: 0.001,
        value: 0,
        orientation: 'horizontal',
        range: "min",
        slide: function(event, ui) {
          $("#tempbasal_amount_slider_label").text(ui.value);
        }
      }).addSliderSegments();
    }

    var $slider = $('#tempbasal_time_slider');
    var sliderValueMultiplier = 1;
    var sliderOptions;

    if ($slider.length > 0) {
      $slider.slider({
        min: 0,
        max: simt,
        step: 30,
        values: [0, 30],
        orientation: 'horizontal',
        range: true,
        slide: function (event, ui) {
          $slider.find('.ui-slider-value:first')
            .text(ui.values[0] * sliderValueMultiplier)
            .end()
            .find('.ui-slider-value:last')
            .text(ui.values[1] * sliderValueMultiplier);
        }
      });

      sliderOptions = $slider.slider('option');
      $slider.addSliderSegments(sliderOptions.max)
        .find('.ui-slider-value:first')
        .text(sliderOptions.values[0] * sliderValueMultiplier)
        .end()
        .find('.ui-slider-value:last')
        .text(sliderOptions.values[1] * sliderValueMultiplier);
    }

    // Disable link clicks to prevent page scrolling
    $(document).on('click', 'a[href="#new_event_link"]', function (e) {
      e.preventDefault();
    });

    // Switches
    // if ($('[data-toggle="switch"]').length) {
    //   $('[data-toggle="switch"]').bootstrapSwitch();
    // }

    if ( userdata.stats == 1 ) {
      $('#show_statistics').bootstrapSwitch('state' , true);
    } else {
      $('#show_statistics').bootstrapSwitch();      
    }
    
    if ( userdata.inputeffect == 1 ) {
      $('#show_input_effects').bootstrapSwitch('state' , true);
    } else {
      $('#show_input_effects').bootstrapSwitch();      
    }
    
    // make code pretty
    window.prettyPrint && prettyPrint();

  });

})(jQuery);
