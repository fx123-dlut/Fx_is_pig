package org.apache.archiva.transaction;

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

import java.io.IOException;

/**
 * Interface for individual events in a transaction.
 *
 */
public interface TransactionEvent
{
    /**
     * Commit this event.
     *
     * @throws IOException if an error occurred committing the change
     */
    void commit()
        throws IOException;

    /**
     * Rollback the even already committed.
     *
     * @throws IOException if an error occurred reverting the change
     */
    void rollback()
        throws IOException;
}
