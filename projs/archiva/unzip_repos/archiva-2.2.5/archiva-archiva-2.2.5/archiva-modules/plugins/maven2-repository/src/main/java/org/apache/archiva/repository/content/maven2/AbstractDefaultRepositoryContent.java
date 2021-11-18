package org.apache.archiva.repository.content.maven2;

/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import org.apache.archiva.common.utils.VersionUtil;
import org.apache.archiva.metadata.repository.storage.RepositoryPathTranslator;
import org.apache.archiva.metadata.repository.storage.maven2.ArtifactMappingProvider;
import org.apache.archiva.metadata.repository.storage.maven2.Maven2RepositoryPathTranslator;
import org.apache.archiva.model.ArchivaArtifact;
import org.apache.archiva.model.ArtifactReference;
import org.apache.archiva.model.ProjectReference;
import org.apache.archiva.model.VersionedReference;
import org.apache.archiva.repository.content.PathParser;
import org.apache.archiva.repository.layout.LayoutException;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.PostConstruct;
import javax.inject.Inject;
import java.util.List;

/**
 * AbstractDefaultRepositoryContent - common methods for working with default (maven 2) layout.
 */
public abstract class AbstractDefaultRepositoryContent
{
    protected Logger log = LoggerFactory.getLogger( getClass() );

    public static final String MAVEN_METADATA = "maven-metadata.xml";

    protected static final char PATH_SEPARATOR = '/';

    protected static final char GROUP_SEPARATOR = '.';

    protected static final char ARTIFACT_SEPARATOR = '-';

    private RepositoryPathTranslator pathTranslator = new Maven2RepositoryPathTranslator();

    private PathParser defaultPathParser = new DefaultPathParser();

    /**
     *
     */
    @Inject
    protected List<? extends ArtifactMappingProvider> artifactMappingProviders;

    @PostConstruct
    protected void initialize()
    {
        // no op
    }

    public ArtifactReference toArtifactReference( String path )
        throws LayoutException
    {
        return defaultPathParser.toArtifactReference( path );
    }

    public String toMetadataPath( ProjectReference reference )
    {
        StringBuilder path = new StringBuilder();

        path.append( formatAsDirectory( reference.getGroupId() ) ).append( PATH_SEPARATOR );
        path.append( reference.getArtifactId() ).append( PATH_SEPARATOR );
        path.append( MAVEN_METADATA );

        return path.toString();
    }

    public String toMetadataPath( VersionedReference reference )
    {
        StringBuilder path = new StringBuilder();

        path.append( formatAsDirectory( reference.getGroupId() ) ).append( PATH_SEPARATOR );
        path.append( reference.getArtifactId() ).append( PATH_SEPARATOR );
        if ( reference.getVersion() != null )
        {
            // add the version only if it is present
            path.append( VersionUtil.getBaseVersion( reference.getVersion() ) ).append( PATH_SEPARATOR );
        }
        path.append( MAVEN_METADATA );

        return path.toString();
    }

    public String toPath( ArchivaArtifact reference )
    {
        if ( reference == null )
        {
            throw new IllegalArgumentException( "ArchivaArtifact cannot be null" );
        }

        String baseVersion = VersionUtil.getBaseVersion( reference.getVersion() );
        return toPath( reference.getGroupId(), reference.getArtifactId(), baseVersion, reference.getVersion(),
                       reference.getClassifier(), reference.getType() );
    }

    public String toPath( ArtifactReference reference )
    {
        if ( reference == null )
        {
            throw new IllegalArgumentException( "Artifact reference cannot be null" );
        }
        if ( reference.getVersion() != null )
        {
            String baseVersion = VersionUtil.getBaseVersion( reference.getVersion() );
            return toPath( reference.getGroupId(), reference.getArtifactId(), baseVersion, reference.getVersion(),
                           reference.getClassifier(), reference.getType() );
        }
        return toPath( reference.getGroupId(), reference.getArtifactId(), null, null,
                       reference.getClassifier(), reference.getType() );
    }

    private String formatAsDirectory( String directory )
    {
        return directory.replace( GROUP_SEPARATOR, PATH_SEPARATOR );
    }

    private String toPath( String groupId, String artifactId, String baseVersion, String version, String classifier,
                           String type )
    {
        if ( baseVersion != null )
        {
            return pathTranslator.toPath( groupId, artifactId, baseVersion,
                                          constructId( artifactId, version, classifier, type ) );
        }
        else
        {
            return pathTranslator.toPath( groupId, artifactId );
        }
    }

    // TODO: move into the Maven Artifact facet when refactoring away the caller - the caller will need to have access
    //       to the facet or filename (for the original ID)
    private String constructId( String artifactId, String version, String classifier, String type )
    {
        String ext = null;
        for ( ArtifactMappingProvider provider : artifactMappingProviders )
        {
            ext = provider.mapTypeToExtension( type );
            if ( ext != null )
            {
                break;
            }
        }
        if ( ext == null )
        {
            ext = type;
        }

        StringBuilder id = new StringBuilder();
        if ( ( version != null ) && ( type != null ) )
        {
            id.append( artifactId ).append( ARTIFACT_SEPARATOR ).append( version );

            if ( StringUtils.isNotBlank( classifier ) )
            {
                id.append( ARTIFACT_SEPARATOR ).append( classifier );
            }

            id.append( "." ).append( ext );
        }
        return id.toString();
    }
}
