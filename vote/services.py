from vote.models import Vote

class VoteService():
    def has_user_voted_for_song(self, song, user):
        try:
            Vote.objects.get(song_id=song.id, user_id=user.id)
            return True
        except Vote.DoesNotExist:
            return False
        except Vote.MultipleObjectsReturned:
            return True
    
    def get_users_vote_for_song(self, song, user):
        try:
            vote = Vote.objects.get(song_id=song.id, user_id=user.id)
            return vote
        except Vote.DoesNotExist:
            return None
        except Vote.MultipleObjectsReturned:
            return None