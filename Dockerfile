# Use the official PHP image
FROM php:8.2-apache

# Copy all project files into the container
COPY . /var/www/html/

# Expose web port
EXPOSE 80

# Start Apache automatically
CMD ["apache2-foreground"]