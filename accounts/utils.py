from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, is_superuser, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        
        email = self.normalize_email(email)

        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            is_superuser = is_superuser,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name, last_name, password, False, **extra_fields)
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name, last_name, password, True, **extra_fields)

        

