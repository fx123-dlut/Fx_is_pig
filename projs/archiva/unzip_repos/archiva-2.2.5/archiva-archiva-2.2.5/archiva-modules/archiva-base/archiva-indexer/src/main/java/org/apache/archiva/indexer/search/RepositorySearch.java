package org.apache.archiva.indexer.search;

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

import org.apache.archiva.admin.model.RepositoryAdminException;

import java.util.Collection;
import java.util.List;
import java.util.Set;


public interface RepositorySearch
{
    /**
     * Quick search by won't return artifact with file extension pom
     *
     * @param principal
     * @param selectedRepos
     * @param term
     * @param limits
     * @param previousSearchTerms
     * @return
     */
    SearchResults search( String principal, List<String> selectedRepos, String term, SearchResultLimits limits,
                          List<String> previousSearchTerms )
        throws RepositorySearchException;

    /**
     * Advanced search.
     *
     * @param principal
     * @param searchFields
     * @param limits
     * @return
     */
    SearchResults search( String principal, SearchFields searchFields, SearchResultLimits limits )
        throws RepositorySearchException;

    Collection<String> getAllGroupIds( String principal, List<String> selectedRepos )
        throws RepositorySearchException;

    Set<String> getRemoteIndexingContextIds( String managedRepoId )
        throws RepositoryAdminException;
}
