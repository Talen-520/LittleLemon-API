from rest_framework.throttling import UserRateThrottle
#with this class, all auth user can make 10 calls per minute
class TenCallsPerMinute(UserRateThrottle):
    scope = 'ten'