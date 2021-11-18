package org.apache.archiva.test.utils;

/*
 * Copyright 2012 The Apache Software Foundation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import org.junit.runners.BlockJUnit4ClassRunner;
import org.junit.runners.model.FrameworkMethod;
import org.junit.runners.model.InitializationError;

import java.util.List;

/**
 * @author Eric
 */
public class ArchivaBlockJUnit4ClassRunner
    extends BlockJUnit4ClassRunner
{

    public ArchivaBlockJUnit4ClassRunner( Class<?> klass )
        throws InitializationError
    {
        super( klass );
    }

    @Override
    protected List<FrameworkMethod> computeTestMethods()
    {
        return ListGenerator.getShuffleList( super.computeTestMethods() );
    }
}
