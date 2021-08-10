from lib.base import BaseReviewBoardAction

__all__ = [
    'UpdateReviewStatus'
]


class UpdateReviewStatus(BaseReviewBoardAction):
    def run(self, review, status, reason):
        review_request = self._client.get_review_request(review_request_id=review)

        payload = {
            'status': status
        }

        if review_request.status != status:
            if status != 'pending':
                payload['close_description'] = reason
            review_request = review_request.update(**payload)
        return review_request.status == status
