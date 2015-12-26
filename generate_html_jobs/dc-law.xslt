<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns0="http://www.w3.org/2001/XInclude">
  <xsl:output method="html" doctype-system="about:legacy-compat" />
  <xsl:param name="genpath" />
  <xsl:template match="/">
    <html class="no-js">
      <head>
          <meta charset='utf-8' />
          <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1' />
          <title>DC Code - <xsl:apply-templates select="$genpath/heading" /></title>
          <meta property='st:title' content="{./*/cache/title}" />
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
            <h1 id="sitename"><a href="/">
              Code of the District of Columbia (Unofficial)
            </a></h1>
          </div>
        </header>
        <div class="main container">
          <div class="clearfix" style="width: 100%;">
            <div id="sidebar" class="col4 quiet">
              <xsl:apply-templates select="./*/cache/ancestors" />
              <xsl:apply-templates select="./*/cache/siblings/prev" />
              <xsl:apply-templates select="./*/cache/siblings/next" />
              <xsl:if test="$genpath/ancestor::code">
                <xsl:call-template name="genNav" />
              </xsl:if>
              <xsl:apply-templates select="//recency[1]" />
            </div>
            <div class="col8">
              <div id="content">
                <xsl:apply-templates select="$genpath" />
              </div>
            </div>
          </div>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="section">
    <xsl:value-of select="num" />. <xsl:value-of select="heading" />
  </xsl:template>

<!-- CONTAINERS -->

  <xsl:template match="code">
    <div class="line-group line-group-page-heading">
      <h1 data-swiftype-index="true">
        <xsl:apply-templates select="heading" />
      </h1>
    </div>
    <div class="line-group toc" data-swiftype-index="true">
        <xsl:for-each select="container">
          <xsl:call-template name="makeTOC">
            <xsl:with-param name="node" select="." />
          </xsl:call-template>
        </xsl:for-each>
    </div>
  </xsl:template>

  <xsl:template match="container">
    <div class="line-group line-group-page-heading">
      <h1 data-swiftype-index="true">
        <xsl:apply-templates select="heading" />
      </h1>
    </div>
    <div class="line-group toc" data-swiftype-index="true">
      <xsl:for-each select="container|section">
        <xsl:call-template name="makeTOC">
          <xsl:with-param name="node" select="." />
        </xsl:call-template>
      </xsl:for-each>
    </div>
  </xsl:template>

  <xsl:template name="makeTOC">
    <xsl:param name="node" />
    <xsl:choose>
      <!-- create heading for Divisions/Subtitles; iterate over children -->
      <xsl:when test="$node/parent::*[@childPrefix = 'Division' or @childPrefix = 'Subtitle']">
        <div class="line subheading" style="text-indent: 0em;">
          <p>
            <xsl:apply-templates select="heading" />
          </p>
        </div>
        <xsl:for-each select="container|section">
          <xsl:call-template name="makeTOC">
            <xsl:with-param name="node" select="." />
          </xsl:call-template>
        </xsl:for-each>
      </xsl:when>
      <!-- create link to everything else -->
      <xsl:otherwise>
        <div class="line child-link " style="text-indent: 0em">
          <div>
            <span class="title">
              <xsl:call-template name="genLink">
                <xsl:with-param name="node" select="." />
                <xsl:with-param name="internal" select="true()" />
              </xsl:call-template>
            </span>
          </div>
          <xsl:if test="(.//section)[1]">
            <div>
              <span class="range">
                §§ <xsl:value-of select="(.//section)[1]/num" /> - <xsl:value-of select="(.//section)[last()]/num" />
              </span>
            </div>
          </xsl:if>
        </div>

      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

<!-- SIDEBAR NAV -->

  <xsl:template name="genNav">
    <h2>You Are Here</h2>
    <ul class="ancestors">
      <a href="/">Code of the District of Columbia</a>
      <xsl:for-each select="$genpath/ancestor::container[not(../@childPrefix = 'Division' or ../@childPrefix = 'Subtitle')]">
        <li>↪ <xsl:call-template name="genLink">
          <xsl:with-param name="node" select="." />
          <xsl:with-param name="internal" select="false()" />
        </xsl:call-template></li>
      </xsl:for-each>
      <li>
        ↪ <xsl:apply-templates select="$genpath/heading" />
      </li>
    </ul>

    <xsl:call-template name="genPrev">
      <xsl:with-param name="node" select="$genpath" />
    </xsl:call-template>

    <xsl:call-template name="genNext">
      <xsl:with-param name="node" select="$genpath" />
    </xsl:call-template>
  </xsl:template>


  <xsl:template name="genPrev">
    <xsl:param name="node" />
    <xsl:if test="$node/ancestor::code">
      <h2>Previous</h2>
      <xsl:choose>
        <xsl:when test="$node/preceding-sibling::*[self::container or self::section][1]">
          <p><xsl:call-template name="genLink">
            <xsl:with-param name="node" select="$node/preceding-sibling::*[self::container or self::section][1]" />
          </xsl:call-template></p>
        </xsl:when>
        <xsl:when test="$node/parent::*[../@childPrefix = 'Division' or ../@childPrefix = 'Subtitle']/preceding-sibling::container[1]/*[self::container or self::section][last()]">
          <p><xsl:call-template name="genLink">
            <xsl:with-param name="node" select="$node/parent::*[../@childPrefix = 'Division' or ../@childPrefix = 'Subtitle']/preceding-sibling::container[1]/*[self::container or self::section][last()]" />
          </xsl:call-template></p>
        </xsl:when>
        <xsl:when test="$node/parent::*[../@childPrefix = 'Division' or ../@childPrefix = 'Subtitle']/..">
          <p><xsl:call-template name="genLink">
            <xsl:with-param name="node" select="$node/parent::*[../@childPrefix = 'Division' or ../@childPrefix = 'Subtitle']/.." />
          </xsl:call-template></p>
        </xsl:when>
        <xsl:otherwise>
          <p><xsl:call-template name="genLink">
            <xsl:with-param name="node" select="$node/.." />
          </xsl:call-template></p>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
  </xsl:template>

  <xsl:template name="genNext">
    <xsl:param name="node" />
    <xsl:variable name="next" select="$node/following-sibling::*[self::container or self::section][1]" />
    <xsl:choose>
      <xsl:when test="not($node/ancestor::code)"></xsl:when>
      <xsl:when test="($next) and ($node/parent::*[@childPrefix = 'Division' or @childPrefix = 'Subtitle'])">
        <h2>Next</h2>
        <p><xsl:call-template name="genLink">
          <xsl:with-param name="node" select="$next/*[self::container or self::section][1]" />
        </xsl:call-template></p>
      </xsl:when>
      <xsl:when test="$next">
        <h2>Next</h2>
        <p><xsl:call-template name="genLink">
          <xsl:with-param name="node" select="$next" />
        </xsl:call-template></p>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="genNext">
          <xsl:with-param name="node" select="$node/.." />
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

<!-- RECENCY -->

  <xsl:template match="recency">
    <h2>Publication Information</h2>
    <h3>Current through <xsl:call-template name="formatDate"><xsl:with-param name="date" select="./law/effective" /></xsl:call-template></h3>
      <dl id="recency">
        <dt>Last codified D.C. Law:</dt>
        <dd>
          Law <xsl:value-of select="./law/law" /> effective <xsl:call-template name="formatDate"><xsl:with-param name="date" select="./law/effective" /></xsl:call-template>
        </dd>
        <dt>Last codified Emergency Law:</dt>
        <dd>
          Act <xsl:value-of select="./emergency/law" /> effective <xsl:call-template name="formatDate"><xsl:with-param name="date" select="./emergency/effective" /></xsl:call-template>
        </dd>
        <dt>Last codified Federal Law:</dt>
        <dd>
          Public Law <xsl:value-of select="./federal/law" /> approved <xsl:call-template name="formatDate"><xsl:with-param name="date" select="./federal/effective" /></xsl:call-template>
        </dd>
      </dl>
  </xsl:template>


<!-- HELPERS -->

  <xsl:template match="heading">
    <xsl:choose>
      <xsl:when test="parent::section">
        § <xsl:value-of select="../num" />. 
      </xsl:when>
      <xsl:when test="../../@childPrefix">
        <xsl:value-of select="../../@childPrefix" /><xsl:text> </xsl:text><xsl:value-of select="../num" />. 
      </xsl:when>
    </xsl:choose>
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:variable name="monthLookup" select="document('monthLookup.xml')" />

  <xsl:template name="formatDate">
    <xsl:param name="date" />
    <xsl:variable name="year" select="substring($date, 1, 4)" />
    <xsl:variable name="month" select="substring($date, 6, 2)" />
    <xsl:variable name="monthName" select="$monthLookup/months/month[@num=number($month)]" />
    <xsl:variable name="day" select="substring($date, 9, 2)" />
    <xsl:value-of select="concat($monthName, ' ', $day, ', ', $year)" />
  </xsl:template>

  <xsl:template name="genUrl">
    <xsl:param name="node" />
    <xsl:choose>
      <xsl:when test="$node/self::code">/</xsl:when>
      <xsl:when test="$node/self::section">/sections/<xsl:value-of select="$node/num" /></xsl:when>
      <xsl:when test="$node/parent::*[@childPrefix = 'Division' or @childPrefix = 'Subtitle']">
        <xsl:call-template name="genUrl">
          <xsl:with-param name="node" select="$node/.." />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise><xsl:call-template name="genUrl">
          <xsl:with-param name="node" select="$node/.." />
        </xsl:call-template><xsl:value-of select="$node/../@childPrefix" />-<xsl:value-of select="$node/num" />/</xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="genLink">
    <xsl:param name="node" />
    <xsl:param name="internal" />
    <a>
      <xsl:if test="$internal">
        <xsl:attribute name="class">internal-link</xsl:attribute>
      </xsl:if>
      <xsl:attribute name="href">
        <xsl:call-template name="genUrl">
          <xsl:with-param name="node" select="$node" />
        </xsl:call-template>
      </xsl:attribute>
      <xsl:apply-templates select="$node/heading" />
    </a>
  </xsl:template>

</xsl:stylesheet>
