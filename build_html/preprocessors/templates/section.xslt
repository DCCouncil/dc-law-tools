<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns0="http://www.w3.org/2001/XInclude">
  <xsl:output method="html" doctype-system="about:legacy-compat" />

<!-- RECENCY -->

  <xsl:template match="recency">
    <div>
      <h2>Publication Information</h2>
      <h3>Current through <xsl:value-of select="./law/effective" /></h3>
        <dl id="recency">
          <dt>Last codified D.C. Law:</dt>
          <dd>
            Law <xsl:value-of select="law/law" /> effective <xsl:value-of select="law/effective" />
          </dd>
          <dt>Last codified Emergency Law:</dt>
          <dd>
            Act <xsl:value-of select="emergency/law" /> effective <xsl:value-of select="emergency/effective" />
          </dd>
          <dt>Last codified Federal Law:</dt>
          <dd>
            Public Law <xsl:value-of select="./federal/law" /> approved <xsl:value-of  select="federal/effective" />
          </dd>
        </dl>
      </div>
  </xsl:template>

<!-- SECTION -->

  <xsl:template match="section[text or para or afterText or annotations/annoGroup]">
    <div>
      <xsl:if test="text | para | afterText">
        <div class="line-group primary-content">
          <xsl:apply-templates select="text | para | afterText" />
        </div>
      </xsl:if>
      <xsl:if test="annotations/annoGroup">
        <div class="line-group annotations">
          <xsl:apply-templates select="annotations/annoGroup" />
        </div>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:template match="text | afterText">
    <div class="line" style="text-indent: 1.25em">
      <xsl:apply-templates select="node()" />
    </div>
  </xsl:template>

  <xsl:template match="*[ancestor::text or ancestor::afterText]">
    <xsl:copy-of select="." />
  </xsl:template>


  <xsl:template match="para">
    <xsl:if test="../text | ../heading | preceding-sibling::para">
      <div class="line" style="text-indent: {(count(./ancestor::para) + 1) * 1.25}em">
        <p>
          <xsl:apply-templates select="num" />
        </p>
      </div>
    </xsl:if>
    <xsl:choose>
      <xsl:when test="text | heading">
        <xsl:apply-templates select="para | text[position()>1] | afterText" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="para | afterText"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="num[ancestor::para]">
    <span class="level-num">
      <xsl:value-of select="." />
    </span>
    <xsl:choose>
      <xsl:when test="following-sibling::text | following-sibling::heading">
        <xsl:if test="following-sibling::heading">
          <span class="level-heading">
            <xsl:value-of select="following-sibling::heading" />
          </span> 
        </xsl:if>
        <span><xsl:value-of select="following-sibling::text" /></span>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="../para[1]/num" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="cache"></xsl:template>

  <xsl:template match="annoGroup[heading/text()='History']">
    <div class="line" style="text-indent: 1.5em">
      (<xsl:apply-templates select="./annotation" />.)
    </div>
  </xsl:template>

  <xsl:template match="annoGroup[heading/text()='History']/annotation">
    <xsl:if test="position()>1">; </xsl:if><xsl:choose>
      <xsl:when test="@url"><a class="internal-link" href="{@url}"><xsl:value-of select="." /></a></xsl:when>
      <xsl:otherwise><xsl:value-of select="." /></xsl:otherwise></xsl:choose>
  </xsl:template>
  
  <xsl:template match="annoGroup">
    <div class="line subheading">
      <xsl:value-of select="heading" />
    </div>
    <xsl:for-each select="text | annotation">
      <div class="line" style="text-indent: 1.5em">
        <xsl:value-of select='.' />
      </div>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
