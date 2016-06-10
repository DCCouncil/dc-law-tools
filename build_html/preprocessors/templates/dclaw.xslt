<?xml version="1.0"?><xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns0="http://www.w3.org/2001/XInclude">
  <xsl:output method="html" doctype-system="about:legacy-compat" />

  <xsl:include href="./base.xslt" />

  <xsl:template match="document" mode="meta">
    <h2>Law Information</h2>
    <dl>
      <dt>Cites</dt>
      <dd>
        <xsl:apply-templates select="cites/*" />
      </dd>
      <dt>Effective</dt>
      <dd><xsl:value-of select="cache/effective" /></dd>
      <xsl:apply-templates select="history" />
    </dl>
  </xsl:template>

  <xsl:template match="cites">
    <xsl:apply-templates select="*" />
  </xsl:template>

  <xsl:template match="law">
      <dd>D.C. Law <xsl:value-of select="@session" />-<xsl:value-of select="@lawId" /><xsl:if test="@url"> (<a class="internal-link" href="{@url}">PDF</a>)</xsl:if></dd>
  </xsl:template>

  <xsl:template match="register">
    <xsl:choose>
      <xsl:when test="@url">
        <dd><a href="{@url}"><xsl:value-of select="@vol" /> DCR <xsl:value-of select="@page" /></a></dd>
      </xsl:when>
      <xsl:otherwise>
        <dd><xsl:value-of select="@vol" /> DCR <xsl:value-of select="@page" /></dd>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="history">
    <dt>Legislative History<xsl:if test="@url"> (<a href="{@url}">LIMS</a>)</xsl:if></dt>
    <xsl:apply-templates select="narrative" />
  </xsl:template>

  <xsl:template match="narrative">
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>
</xsl:stylesheet>
