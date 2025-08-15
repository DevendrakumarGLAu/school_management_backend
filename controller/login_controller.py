from django.contrib.auth.hashers import check_password
from login.models import UserAccount
from fastapi import HTTPException

class LoginController:

    @staticmethod
    def login_user(email: str, password: str):
        try:
            user = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")

        if not check_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # In a real app, generate and return a JWT here
        return {
            "message": "Login successful",
            "user_id": user.id,
            "role": getattr(user, "role", "student")  # assuming role field exists
        }
