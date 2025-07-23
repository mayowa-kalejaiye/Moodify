# Legacy Tools

This directory contains obsolete tools and scripts that were used during early development phases or for one-time fixes. These scripts are kept for historical reference but should not be used in the current codebase.

## Contents

### Database Fix Scripts

- `fix_database.py` - Early database schema repair script
- `fix_database_direct.py` - Direct database intervention script
- `fix_database_schema.py` - Schema correction utility
- `fix_migrations.py` - Migration repair tool
- `fix_challenge_table.py` - Challenge table structure fix
- `fix_cointransaction_table.py` - CoinTransaction table repair

### Debugging Tools

- `debug_challenge_table.py` - Challenge table debugging utility
- `debug_profile_update.py` - Profile update debugging tool

## Usage Warning

**CAUTION**: These scripts should NOT be run on the current database as they may cause data corruption or unexpected behavior. They are maintained only for documentation and historical reference.
