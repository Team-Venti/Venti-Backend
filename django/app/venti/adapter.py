from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def __init__(self,*args,**kwargs):
        super(CustomAccountAdapter, self).__init__(*args, **kwargs)

    def save_user(self, request, user, form, commit=False):
        user = super(CustomAccountAdapter,self).save_user(request, user, form, commit)
        data = form.cleaned_data
        user.nickname = data.get('nickname')
        user.gender = data.get('gender')
        user.birth = data.get('birth')
        user.save()
        return user