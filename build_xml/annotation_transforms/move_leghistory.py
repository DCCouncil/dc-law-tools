"""
Move legislative history nodes into the proper statute stub node.

Delete legislative history nodes that are just references to other legislative history nodes elsewhere in the code.

    ...
    <statute stub="true">
      ...
      <legislativeHistory>
        <narrative>
          {text of legislative history node}
        </narrative>
      </legislativeHistory>
    </statute>
"""

def move_leghistory(dom):
    print('  move_leghistory not implemented yet')
