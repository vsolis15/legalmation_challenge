from app import app
from db_methods import insert_file, get_files, get_file_by_name, get_file_by_id

name_d = 'D.xml'
plaintiff_d = 'John Smith'
defendant_d = 'Sally James'

name_e = 'E.xml'
plaintiff_e = 'Juan Garcia'
defendant_e = 'Jessica Jones'

name_f = 'F.xml'
plaintiff_f = 'Jose Rivas'
defendant_f = 'Vanessa Ponce'


def test_db():
    
    insert_file(name_d, plaintiff_d, defendant_d)
    insert_file(name_e, plaintiff_e, defendant_e)
    insert_file(name_f, plaintiff_f, defendant_f)


    file_d = get_file_by_name('D.xml')
    file_e = get_file_by_name('E.xml')
    file_f = get_file_by_name('F.xml')

    file_1 = get_file_by_id(9)
    file_2 = get_file_by_id(10)
    file_3 = get_file_by_id(11)

    files = get_files()

    assert len(files) == 11

    assert file_d[1] == 'D.xml'
    assert file_d[2] == 'John Smith'
    assert file_d[3] == 'Sally James'

    assert file_e[1] == 'E.xml'
    assert file_e[2] == 'Juan Garcia'
    assert file_e[3] == 'Jessica Jones'

    assert file_f[1] == 'F.xml'
    assert file_f[2] == 'Jose Rivas'
    assert file_f[3] == 'Vanessa Ponce'

    assert file_1[1] == 'D.xml'
    assert file_1[2] == 'John Smith'
    assert file_1[3] == 'Sally James'

    assert file_2[1] == 'E.xml'
    assert file_2[2] == 'Juan Garcia'
    assert file_2[3] == 'Jessica Jones'

    assert file_3[1] == 'F.xml'
    assert file_3[2] == 'Jose Rivas'
    assert file_3[3] == 'Vanessa Ponce'

if __name__ == "__main__":
    test_db()