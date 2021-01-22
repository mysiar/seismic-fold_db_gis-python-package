import csv
from sqlalchemy.orm import sessionmaker
from SeismicFoldDbGis.entity.Bin import Bin


class FoldDbGis:

    def __init__(self, db_engine, commit_every: int = 10000):
        self.__db_engine = db_engine
        self.__commit_every = commit_every

    def create_table(self):
        Bin.__table__.create(self.__db_engine)

    def load_from_csv(self, filename: str):
        """
        load from CSV with columns ['Easting', 'Northing', 'Fold', 'Bin Number', 'Row', 'Column']
        """
        _session = self.__create_session()
        counter = 1
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for record in csv_reader:
                bin = FoldDbGis.__create_bin_from_csv_record(record)
                _session.add(bin)

                if self.__commit_every == counter:
                    _session.commit()
                    counter = 1

                counter += 1

            _session.commit()
        _session.close()

    def update_from_csv(self, filename: str):
        """
        update from CSV with columns ['Easting', 'Northing', 'Fold', 'Bin Number', 'Row', 'Column']
        """
        _session = self.__create_session()
        counter = 0
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for record in csv_reader:
                binn = int(record[3])
                b = _session.query(Bin).filter_by(binn=binn).first()

                if b is not None:
                    b.fold = b.fold + int(record[2])
                else:
                    b = FoldDbGis.__create_bin_from_csv_record(record)
                    _session.add(b)

                if self.__commit_every == counter:
                    _session.commit()
                    counter = 0

                counter += 1

            _session.commit()
        _session.close()

    @staticmethod
    def __create_bin_from_csv_record(record: list):
        b = Bin(
            binn=int(record[3]),
            fold=int(record[2]),
            geom="POINT (%.1f %.1f)" % (float(record[0]), float(record[1]))
        )

        return b

    def __create_session(self):
        sess_mkr = sessionmaker()
        sess_mkr.configure(bind=self.__db_engine)
        return sess_mkr()