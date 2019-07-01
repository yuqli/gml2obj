class GeoProcessing:
    def __init__(self):
        self.input_dir = None
    
    def set_input_directory(self,path):
        self.input_dir = path

    def convert_to_lat_long(self):
        from pyproj import Proj, transform
        from itertools import islice 
        import glob
        import csv

        inProj = Proj(init='epsg:2263', preserve_units = True)
        outProj = Proj(init='epsg:4326')
        
        with open('point_cloud.csv', mode='w') as pcf:
            pcw = csv.writer(pcf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for file in glob.glob(self.input_dir + "*.obj"):
                with open(file, 'r') as fin:
                    line = next(islice(fin, 2, 3))
                    words = line.split(' ')
                    northing_local,easting_local = words[-2],words[-1]
                    
                    easting,northing = transform(inProj,outProj,northing_local,easting_local)                    
                    pcw.writerow([file.split("/")[-1], northing, easting])

    def fetch_roi_files(self):
        pass

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='train res-folding net')
    parser.add_argument('-i', '--input-data', type=str, default="./input_gml/", help='fill in the input directory')
    args = parser.parse_args()
    
    GeoProc = GeoProcessing()
    GeoProc.set_input_directory(args.input_data)
    GeoProc.convert_to_lat_long()
