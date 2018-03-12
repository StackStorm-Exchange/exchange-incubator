from lib.base import BaseKayakoAction
import kayako

__all__ = [
    'CreateKayakoIssueAction'
]

class CreateKayakoIssueAction(BaseKayakoAction):

    def run(self, subject, contents, user_email, user_fullname, department,
            status, priority, ticket_type, staff_email = None):
        registered = self._client.first(kayako.UserGroup, title='Registered')
        try:
            customer = self._client.user_search(query=user_email)[0]
        except IndexError:
            customer = self._client.create(User, fullname=user_fullname,
                    password=uuid.uuid4().hex, email=user_email,
                    usergroupid=registered.id, sendwelcomeemail=False)
            customer.add()
        if staff_email:
            staff = self._client.first(kayako.Staff, email=staff_email)
            staff_id = staff.id
            fullname = "%s %s" % ( staff.firstname, staff.lastname )
        else:
            staff_id = None
            fullname = user_fullname

        department = self._client.first(kayako.Department, title=department)
        tickettype = self._client.first(kayako.TicketType, title=ticket_type)
        ticketstatus = self._client.first(kayako.TicketStatus, title=status)
        ticketpriority = self._client.first(kayako.TicketPriority, title=priority)

        ticket = self._client.create(kayako.Ticket)
        ticket.tickettypeid = tickettype.id
        ticket.ticketstatusid = ticketstatus.id
        ticket.ticketpriorityid = ticketpriority.id
        ticket.departmentid = department.id
        if staff_email:
            ticket.staffid = staff_id
        else:
            ticket.userid = customer.id
        ticket.ignoreautoresponder = 1
        ticket.subject = subject
        ticket.fullname = fullname
        ticket.email = user_email
        ticket.contents = contents
        ticket.add()
        return ticket.id


