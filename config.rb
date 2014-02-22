add_import_path "static/bower_components/foundation/scss"

css_dir = "static/css"
sass_dir = "static/scss"
images_dir = "static/img"
javascripts_dir = "static/js"

http_path = "/static/"
http_images_path = "/static/img/"
http_javascripts_path = "static/js/"

# Change this variable to 'production' for compressed css files
environment = :development

# You can select your preferred output style here (can be overridden via the command line):
# output_style = :expanded or :nested or :compact or :compressed
if environment == :development
  line_comments = true
  output_style = :nested
  sass_options = {:debug_info => true}
else
  line_comments = false
  output_style = :compressed
  sass_options = {:debug_info => false}
end

# To enable relative paths to assets via compass helper functions. Uncomment:
relative_assets = true


# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass sass scss && rm -rf sass && mv scss sass
