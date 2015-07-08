from openerp.addons.web import controllers
controllers.main.html_template = """<!DOCTYPE html>
<html style="height: 100%%">
  <head>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>OpenEduCat</title>
    <link rel="shortcut icon"
          href="/openeducat_erp/static/src/img/openeducat_favicon.png"
          type="image/x-icon"/>
    <link rel="stylesheet" href="/web/static/src/css/full.css" />
      %(css)s
      %(js)s
    <script type="text/javascript">
      $(function() {
        var s = new openerp.init(%(modules)s);
        %(init)s
      });
    </script>
  </head>
  <body>
    <!--[if lte IE 8]>
    <script
      src="//ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js">
    </script>
    <script>CFInstall.check({mode: "overlay"});</script>
    <![endif]-->
    </body>
</html>
"""
