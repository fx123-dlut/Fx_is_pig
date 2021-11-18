package org.apache.archiva.rest.services.utils;
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import org.apache.archiva.common.plexusbridge.PlexusSisuBridge;
import org.apache.maven.index.NexusIndexer;
import org.apache.maven.index.context.IndexingContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.PreDestroy;
import javax.inject.Inject;

/**
 * @author Olivier Lamy
 */
@Service
public class MavenIndexerCleaner
{
    Logger log = LoggerFactory.getLogger( getClass() );

    @Inject
    private PlexusSisuBridge plexusSisuBridge;

    @PreDestroy
    public void shutdown()
        throws Exception
    {

        log.info( "cleanup IndexingContext" );
        NexusIndexer nexusIndexer = plexusSisuBridge.lookup( NexusIndexer.class );
        for ( IndexingContext context : nexusIndexer.getIndexingContexts().values() )
        {
            nexusIndexer.removeIndexingContext( context, true );
        }
    }
}
