from core.models import Resource, Review, Feedback

def dashboard_callback(request, context):
    total_resources = Resource.objects.count()
    pending_reviews = Review.objects.filter(status="pending").count()
    pending_feedback = Feedback.objects.filter(status="pending").count()
    recent_feedbacks = Feedback.objects.order_by("-created_at")[:5]
    
    context.update({
        "total_resources": total_resources,
        "pending_reviews": pending_reviews,
        "pending_feedback": pending_feedback,
        "recent_feedbacks": recent_feedbacks,
    })
    
    return context
