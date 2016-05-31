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
          <link href='http://fonts.googleapis.com/css?family=Open+Sans:400italic,700italic,400,700' rel='stylesheet' type='text/css' />
          <link rel='stylesheet' type='text/css' href='/css/reset.css' media='screen' />
          <link rel='stylesheet' type='text/css' href='/css/site.css' media='screen' />
          <link rel='stylesheet' type='text/css' href='/css/body.css' media='screen' />
          <link rel='stylesheet' type='text/css' href='/css/print.css' media='print' />
          <link rel='stylesheet' type='text/css' href='/css/icons/style.css' media='screen' />
      </head>
      <body>
        <header>
          <div class="container">
            <h1 id="sitename"><a href="{*/cache/root/url}">
              <xsl:value-of select="*/cache/root/title | */cache/title[not(../root/title)]" />
            </a></h1>
          </div>
        </header>
        <div class="main container">
          <div class="clearfix" style="width: 100%;">
            <div id="sidebar" class="col4 quiet">
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
      </body>
    </html>
  </xsl:template>

  <xsl:template match="*" mode="toc"></xsl:template>
  <xsl:template match="*" mode="content"></xsl:template>

<!-- SIDEBAR NAV -->

  <xsl:template match="*" mode="meta">
    <xsl:copy-of select="./cache/root/div/*" />
  </xsl:template>

  <xsl:template match="ancestor">
    <li>↪ <a href="{@url}"><xsl:value-of select="@title" /></a></li>
  </xsl:template>

  <xsl:template match="siblings/next">
      <h2>Previous</h2>
      <p><a class="internal-link" href="{@url}"><xsl:value-of select="@title" /></a></p>
  </xsl:template>

  <xsl:template match="siblings/prev">
      <h2>Next</h2>
      <p><a class="internal-link" href="{@url}"><xsl:value-of select="@title" /></a></p>
  </xsl:template>

</xsl:stylesheet>