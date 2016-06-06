<?xml version="1.0"?><xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns0="http://www.w3.org/2001/XInclude">
  <xsl:output method="html" doctype-system="about:legacy-compat" />

  <xsl:template match="/">
    <html class="no-js">
      <head>
          <meta charset='utf-8' />
          <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1' />
          <title>DC Code - <xsl:value-of select="*/cache/title" /></title>
          <meta property='st:title' content="{*/cache/title}" />
          <meta name='description' content='A simple, free browser for the Washington, DC Code' />
          <meta name='viewport' content='width=device-width' />
          <link href='https://fonts.googleapis.com/css?family=Open+Sans:400italic,700italic,400,700' rel='stylesheet' type='text/css' />
          <link rel='stylesheet' type='text/css' href='/css/reset.css' media='screen' />
          <link rel='stylesheet' type='text/css' href='/css/site.css' media='screen' />
          <link rel='stylesheet' type='text/css' href='/css/body.css' media='screen' />
          <link rel='stylesheet' type='text/css' href='/css/print.css' media='print' />
          <link rel='stylesheet' type='text/css' href='/css/icons/style.css' media='screen' />
          <script type="text/javascript">
            var _paq = _paq || [];
            _paq.push(['trackPageView']);
            _paq.push(['enableLinkTracking']);
            (function() {
              var u="//analytics.code.dccouncil.us/";
              _paq.push(['setTrackerUrl', u+'piwik.php']);
              _paq.push(['setSiteId', 1]);
              var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
              g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
            })();

          window.searchHost = 'https://search.code.dccouncil.us';
          window.queryUrl = '/v1/search';
          </script>
          <noscript><p><img src="//analytics.code.dccouncil.us/piwik.php?idsite=1" style="border:0;" alt="" /></p></noscript>
      </head>
      <body>
        <header>
          <div class="container">
            <div class="right no-print search" id="search">&#160;</div>
            <h1 id="sitename"><a href="{*/cache/root/url}">
              <xsl:value-of select="*/cache/root/title | */cache/title[not(../root/title)]" />
            </a></h1>
          </div>
        </header>
        <div class="main container">
          <div class="clearfix" style="width: 100%;">
            <div id="sidebar" class="col4 quiet">
              <div class="cta">
                <p><a class="em" href="mailto:code@dccouncil.us?subject=[ERROR]+{*/cache/url}">Report Error</a></p>
                <p><a href="mailto:code@dccouncil.us?subject=[SUPPORT]+{*/cache/url}">Support Question</a></p>
                <p><a href="mailto:code@dccouncil.us?subject=[FEEDBACK]+{*/cache/url}">Feedback on Beta</a></p>
              </div>
              <h2>You Are Here</h2>
              <ul class="ancestors">
                <xsl:apply-templates select="*/cache/ancestors/ancestor" />
                <li>↪ <xsl:value-of select="*/cache/title" /></li>
              </ul>
              <xsl:apply-templates select="*/cache/siblings/prev" />
              <xsl:apply-templates select="*/cache/siblings/next" />
              <xsl:apply-templates select="*" mode="meta" />
            </div>
            <div class="col8 body">
              <h1>
                <xsl:value-of select="*/cache/title" />
              </h1>
              <div class="toc">
                <xsl:apply-templates select="." mode="toc" />
              </div>
              <div class="content">
                <xsl:apply-templates select="." mode="content" />
              </div>
            </div>
          </div>
        </div>
        <footer>
          <div class="container center">
            <p>The codes and laws on this website are in the public domain.
            </p>
            <p>
              Please do not scrape. Instead, bulk download the <a href="https://github.com/dccouncil/dc-law-html">HTML</a> or <a href="https://github.com/dccouncil/dc-law-xml">XML</a>.
            </p>
          </div>
        </footer>
        <script type="text/javascript" src="/js/search.js">&#160;</script>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="*" mode="toc">&#160;</xsl:template>
  <xsl:template match="*" mode="content">&#160;</xsl:template>

<!-- SIDEBAR NAV -->

  <xsl:template match="*" mode="meta">
    <xsl:copy-of select="./cache/root/div/*" />
  </xsl:template>

  <xsl:template match="ancestor">
    <li>↪ <a href="{@url}"><xsl:value-of select="@title" /></a></li>
  </xsl:template>

  <xsl:template match="siblings/prev">
      <h2>Previous</h2>
      <p><a class="internal-link" href="{@url}"><xsl:value-of select="@title" /></a></p>
  </xsl:template>

  <xsl:template match="siblings/next">
      <h2>Next</h2>
      <p><a class="internal-link" href="{@url}"><xsl:value-of select="@title" /></a></p>
  </xsl:template>

</xsl:stylesheet>