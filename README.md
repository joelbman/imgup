Description
=====

A very simplistic image view-upload system using Django.

Demo: http://joel.kapsi.fi/imgup/

Username: demo, password: test

Features
=====
- Uploading only available to authenticated users
  - Extending Django's default user authentication
- Limiting each individual user's maximium file size and total disk space usage
  - Superusers can set the limits for each individual user through Django administration
- Responsive design
  - The layout works regardless of device or resolution

Requirements
=====

- Pillow
- sorl-thumbnail

Both of these packages can be installed using pip:

pip install packagename


