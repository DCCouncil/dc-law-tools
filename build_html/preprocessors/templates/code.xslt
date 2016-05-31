<?xml version="1.0"?><xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns0="http://www.w3.org/2001/XInclude">
  <xsl:output method="html" doctype-system="about:legacy-compat" />

  <xsl:include href="./base.xslt" />

<!-- SECTION -->
  <xsl:template match="section" mode="toc">
  </xsl:template>
  
  <xsl:template match="section" mode="content">
    <xsl:copy-of select="cache/div" />
  </xsl:template>

<!-- CONTAINERS -->

  <xsl:template match="document | container" mode="toc">
    <div class="line-group toc" data-swiftype-index="true">
        <xsl:apply-templates select="container | section" mode="tocLink" />
    </div>
  </xsl:template>

  <xsl:template match="document | container[starts-with(cache/title, 'Title')]" mode="content">
  </xsl:template>

  <xsl:template match="container" mode="content">
      <hr />
      <xsl:apply-templates select="container | section" mode="tocBody" />
  </xsl:template>

  <xsl:template match="container | section" mode="tocLink">
    <xsl:choose>
      <!-- create heading for Divisions/Subtitles; iterate over children -->
      <xsl:when test="cache/noPage">
        <div class="line subheading" style="text-indent: 0em;">
          <p><xsl:value-of select="cache/title" /></p>
        </div>
        <xsl:apply-templates select="container | section" mode="tocLink" />
      </xsl:when>
      <!-- create link to everything else -->
      <xsl:otherwise>
        <div class="line child-link " style="text-indent: 0em">
          <div>
            <span class="title">
              <a class="internal-link" href="{cache/url}">
                <xsl:value-of select="cache/title" />
              </a>
            </span>
          </div>
          <xsl:if test="cache/section-start">
            <div>
              <span class="range">
                §§ <xsl:value-of select="cache/section-start" /> - <xsl:value-of select="cache/section-end" />
              </span>
            </div>
          </xsl:if>
        </div>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match = "container" mode="tocBody">
    <div class="line heading heading-{count(ancestor::container)}" style="text-indent: 0em">
      <p><span class="" style=""><xsl:value-of select="cache/title" /></span></p>
    </div>
    <xsl:apply-templates select="container | section" mode="tocBody" />

  </xsl:template>

  <xsl:template match = "section" mode="tocBody">
    <div class="line heading heading-{count(ancestor::container)}" style="text-indent: 0em">
      <p><span class="" style=""><xsl:value-of select="cache/title" /></span></p>
    </div>
    <xsl:apply-templates select="." mode="content" />
    <hr />
  </xsl:template>

</xsl:stylesheet>
