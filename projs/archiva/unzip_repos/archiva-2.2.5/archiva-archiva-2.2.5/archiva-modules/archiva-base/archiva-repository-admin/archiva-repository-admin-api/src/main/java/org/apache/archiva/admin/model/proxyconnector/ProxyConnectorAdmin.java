package org.apache.archiva.admin.model.proxyconnector;
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

import org.apache.archiva.admin.model.AuditInformation;
import org.apache.archiva.admin.model.RepositoryAdminException;
import org.apache.archiva.admin.model.beans.ProxyConnector;

import java.util.List;
import java.util.Map;

/**
 * <b>No update method for changing source and target here as id is : sourceRepoId and targetRepoId, use delete then add.</b>
 *
 * @author Olivier Lamy
 * @since 1.4-M1
 */
public interface ProxyConnectorAdmin
{
    List<ProxyConnector> getProxyConnectors()
        throws RepositoryAdminException;

    ProxyConnector getProxyConnector( String sourceRepoId, String targetRepoId )
        throws RepositoryAdminException;

    Boolean addProxyConnector( ProxyConnector proxyConnector, AuditInformation auditInformation )
        throws RepositoryAdminException;

    Boolean deleteProxyConnector( ProxyConnector proxyConnector, AuditInformation auditInformation )
        throws RepositoryAdminException;

    /**
     * <b>only for enabled/disable or changing bean values except target/source</b>
     *
     * @param proxyConnector
     * @param auditInformation
     * @return
     * @throws RepositoryAdminException
     */
    Boolean updateProxyConnector( ProxyConnector proxyConnector, AuditInformation auditInformation )
        throws RepositoryAdminException;

    /**
     * @return key/value : managed repo Id / list to proxy connector ordered
     * @throws RepositoryAdminException
     */
    Map<String, List<ProxyConnector>> getProxyConnectorAsMap()
        throws RepositoryAdminException;

}
