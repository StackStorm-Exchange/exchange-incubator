from lib.base import BaseKayakoAction
import kayako

__all__ = [
    'CreateKayakoIssueAction'
]

class CreateKayakoIssueAction(BaseKayakoAction):

    def run(self, ticket_id, contents, staff_email):
        staff = self._client.first(kayako.Staff, email=staff_email)

        ticketpost = self._client.create(kayako.TicketPost)
        ticketpost.ticketid = ticket_id
        ticketpost.contents = contents
        ticketpost.staffid = staff.id
        ticketpost.isprivate = 0
        ticketpost.add()
        return ticketpost.id
