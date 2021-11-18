package org.apache.archiva.rest.services;
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

import org.apache.archiva.admin.model.beans.ManagedRepository;
import org.apache.archiva.admin.model.beans.RepositoryGroup;
import org.apache.archiva.rest.api.services.ManagedRepositoriesService;
import org.apache.archiva.rest.api.services.RepositoryGroupService;
import org.apache.cxf.jaxrs.client.WebClient;
import org.junit.Test;

import java.util.Arrays;

/**
 * @author Olivier Lamy
 */
public class RepositoryGroupServiceTest
    extends AbstractArchivaRestTest
{
    @Test
    public void addAndDelete()
        throws Exception
    {
        RepositoryGroupService service = getRepositoryGroupService();
        WebClient.client( service ).header( "Authorization", authorizationHeader );
        WebClient.client(service).header("Referer","http://localhost:"+port);

        WebClient.getConfig( service ).getHttpConduit().getClient().setReceiveTimeout( 300000 );

        assertTrue( service.getRepositoriesGroups().isEmpty() );

        ManagedRepositoriesService managedRepositoriesService = getManagedRepositoriesService( authorizationHeader );

        WebClient.getConfig( service ).getHttpConduit().getClient().setReceiveTimeout( 300000 );

        ManagedRepository managedRepository = getTestManagedRepository();

        managedRepositoriesService.addManagedRepository( managedRepository );

        RepositoryGroup repositoryGroup = new RepositoryGroup( "one", Arrays.asList( managedRepository.getId() ) )
                .mergedIndexTtl( 40 );

        service.addRepositoryGroup( repositoryGroup );
        assertFalse( service.getRepositoriesGroups().isEmpty() );
        assertEquals( 1, service.getRepositoriesGroups().size() );
        assertEquals( 40, service.getRepositoriesGroups().get(0).getMergedIndexTtl() );

        service.deleteRepositoryGroup( "one" );

        assertTrue( service.getRepositoriesGroups().isEmpty() );
        assertEquals( 0, service.getRepositoriesGroups().size() );
    }
}
