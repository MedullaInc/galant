from gallant import fields as gf


class ClientStatus(gf.ChoiceEnum):
    """ Determines Client's place in workflow / pipeline.
    """
    Potential = 0
    Quoted = 1
    Project_Underway = 2
    Pending_Payment = 3
    Closed = 4


class ClientReferral(gf.ChoiceEnum):
    Search = 0
    Paid_Advertisement = 1
    Social_Media = 2
    Client = 3
    Networking = 4
    Word_Of_Mouth = 5
    Other = 6


class ProjectStatus(gf.ChoiceEnum):
    On_Hold = 0
    Pending_Assignment = 1
    Active = 2
    Overdue = 3
    Completed = 4


class ServiceType(gf.ChoiceEnum):
    Branding = 0
    Design = 1
    Architecture = 2
    Advertising = 3
    Production = 4
    Illustration = 5
    Industrial_Design = 6
    Fashion_Design = 7
    Interior_Design = 8


class ServiceStatus(gf.ChoiceEnum):
    On_Hold = 0
    Pending_Assignment = 1
    Active = 2
    Overdue = 3
    Completed = 4
