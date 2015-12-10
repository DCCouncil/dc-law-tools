"""
Each section contains a `History` annotation that, in
parantheses, lists each statute that has changed the section.
Each statute should (but might not always) 

This script first transforms the dom such that:

    <code>...</code>  

becomes:

    <law>
      <code>...</code>
      <statutes>
        <dc>
          <permanent />
          <temporary />
          <emergency />
        </dc>
        <fed />
      </statutes>
    </law>

Then it creates a new <statute> entry for each DC statute that it finds in the history:

    <law><statutes><dc><permanent>
      <statute stub="true">
        <date>DD-MM-YYYY</date>
        <lawNum>XX-XXX</lawNum>
        <billNum>YY-YYY</billNum>
      </statute>
    </permanent></dc></statutes></law>

and a new <statute> entry for each federal law:
TODO: figure out federal statute structure...

    <law><statutes><fed>
      <statute stub="true">
        ???
      </statute>
    </fed></statutes></law>

"""
def make_statutes(dom):
    print('  make_statutes not implemented')
