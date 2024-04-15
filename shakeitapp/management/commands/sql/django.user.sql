INSERT INTO auth_user
(id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name)
VALUES(1, 'pbkdf2_sha256$600000$zrljk00Glz58ycZXwq58Br$uGtQGKKtt8oKyakmkLI1lJPWmAsvK9WvT9D3rVCDRiE=', '{{ now }}', 1, 'admin', '', 'admin@shakeit.su', 1, 1, '{{ now }}', '');
