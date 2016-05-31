<?xml version="1.0"?><xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns0="http://www.w3.org/2001/XInclude">
  <xsl:output method="html" doctype-system="about:legacy-compat" />

  <xsl:include href="./base.xslt" />

  <xsl:template match="library | collection" mode="toc">
    <div class="line-group toc" data-swiftype-index="true">
        <xsl:apply-templates select="collection | document" mode="tocLink" />
    </div>
  </xsl:template>

  <xsl:template match="collection | document" mode="tocLink">
    <xsl:choose>
      <!-- create heading for noPage collections; iterate over children -->
      <xsl:when test="cache/noPage">
        <div class="line subheading" style="text-indent: 0em;">
          <p><xsl:value-of select="cache/title" /></p>
        </div>
        <xsl:apply-templates select="collection | document" mode="tocLink" />
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
        </div>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>