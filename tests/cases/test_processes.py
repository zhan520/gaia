#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc. and Epidemico Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################
import os
import json
import unittest
from zipfile import ZipFile
import gaia
from gaia.preprocess import crop
from gaia.io import readers

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
testfile_path = os.path.join(base_dir, '../data')


class TestGaiaProcesses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config_file = os.path.join(base_dir, '../../gaia/conf/gaia.cfg')
        gaia.get_config(config_file)

    def test_crop_pandas(self):
        """
        Test cropping (within process) for vector inputs
        """
        reader1 = readers.GaiaReader(
            uri=os.path.join(testfile_path, 'iraq_hospitals.geojson'))

        reader2 = readers.GaiaReader(
            uri=os.path.join(testfile_path, 'baghdad_districts.geojson'))

        output = crop(reader1.read(), reader2.read())

        self.assertEquals(len(output.get_data()), 19)

    def test_crop_gdal(self):
        """
        Test cropping (subset process) for vector & raster inputs
        """
        zipfile = ZipFile(os.path.join(testfile_path, '2states.zip'), 'r')
        zipfile.extract('2states.geojson', testfile_path)

        try:
            reader1 = readers.GaiaReader(
                uri=os.path.join(testfile_path, 'globalairtemp.tif'))
            rasterData = reader1.read()

            reader2 = readers.GaiaReader(
                uri=os.path.join(testfile_path, '2states.geojson'))
            vectorData = reader2.read()

            output = crop(rasterData, vectorData)

            self.assertEquals(type(output.get_data()).__name__, 'Dataset')
        finally:
            testfile = os.path.join(testfile_path, '2states.geojson')
            if os.path.exists(testfile):
                os.remove(testfile)
