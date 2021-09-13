from lib.base import BaseReviewBoardAction
from json import dumps as json_dumps


__all__ = [
    'GetReviewById'
]


class GetReviewById(BaseReviewBoardAction):
    def run(self, review):
        review_request = \
            self._client.get_review_request(
                review_request_id=review)

        return json_dumps(review_request)
