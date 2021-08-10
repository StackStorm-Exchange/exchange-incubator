from lib.base import BaseReviewBoardAction

__all__ = [
    'UpdateReview'
]


class UpdateReview(BaseReviewBoardAction):
    def run(self, review, field, value, publish, trivial):
        review_request = self._client.get_review_request(review_request_id=review)

        payload = {
            field: value if value != "None" else None,
        }
        draft = review_request.get_or_create_draft(**payload)

        if publish:
            payload = {
                'public': publish,
                'trivial': trivial,
            }
            draft.update(**payload)
        
        return self._client.get_review_request(review_request_id=review).id
