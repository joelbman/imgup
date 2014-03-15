Description
=====

A very simplistic image view-upload system using Django.
Still in an early stage of development, will provide a demo-link soon.

Features
=====
- Uploading only available to authenticated users
  - Extending Django's default user authentication
- Limiting each individual user's maximium file size and total disk space usage
  - Superusers can set the limits for each individual user through Django administration

Requirements
=====

- Pillow
- sorl-thumbnail

Both of these packages can be installed using pip:

pip install packagename


