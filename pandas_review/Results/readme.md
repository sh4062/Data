### Requirement:
- python-3.4+
- numpy
- pandas-0.22  !important
> Recommend  Anaconda 5

I use anaconda 5 and have tested it in ubuntu 16.04 and windows10.
#### Usage:
```python
python A_merge_Bx
```
#### Args:
- '--filedir'

  type=str, default='./',help='dir for the file'

- '--fileA'

  type=str, default="Table_A", help='name for fileA'

- '--B_pre'

  type=str, default="Table_B", help='prefix of file B',Ex:Table_B* | Table_B1.xls,Table_B2.xls

- '--PrimaryKey'

  type=str, default="c002", help='PrimaryKey'

- '--A_header_index'

  type=int, default=1, help='Index of A\'s header'

- '--B_header_index

  type=int, default=1,help='Index of B\'s header'

- '--G_I'

  type=int, default=39,help='Generate information index size'

- '--output_path'

  type=str, default='./', help='path for output'

- '--output_filename'

  type=str, default='result.xlsx',help='output_filename for output'
