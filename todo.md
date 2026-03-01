1. create a new base file inside models , that shoule be as base class for the rest of classses , as a inheritable model 
- created_at , updated_at , is_delete (boolean) , deleted_at , id uuid



2. add richtext field for the required table , which is mentioned under the db diagram docue


3. i need string rep , repr __repr__ ,

4. learn about, list comprehensiuon and dict comprehension  , apply it 


5. 
Table	Field	Keep Rich Text?
ahjs	guidelines	 YES
utilities	requirements	 YES
codes	description	 YES (upgrade from varchar)
notes	note_description	 YES
formula	description	 YES
labels	description	⚠ Optional


MAIN_APP_VERSION = "v1"
API_VERSION = "1.0.0"  main .py 