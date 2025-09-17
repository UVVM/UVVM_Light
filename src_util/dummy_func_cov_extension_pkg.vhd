library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
use std.textio.all;

package vendor_func_cov_extension_pkg is
  constant C_VENDOR_EXTENSION_IS_ENABLED : boolean := false;

  function vendor_create_coverpoint_var  return integer;
  procedure vendor_func_cov_set_sampling_var (id: integer; path: string);
  procedure vendor_func_cov_set_coverpoint_var (id: integer; path: string);
  procedure vendor_func_cov_sample_coverage (id: integer);
  procedure vendor_func_cov_add_bin (id: integer; name: string; kind: integer; isTran: integer; lval: integer; rval: integer);
  procedure vendor_func_cov_bin_add_value (id: integer; lval: integer; rval: integer);
  function vendor_func_cov_get_bin_hits (id: integer; name: string) return integer;
  procedure vendor_func_cov_clear_coverage (id: integer);

  subtype t_ucdb_cp_handle is integer;
  subtype t_ucdb_bin_index is integer;

  type t_ucdb_range_type is record
    min: integer;
    max: integer;
  end record;

  constant C_UCDB_ACTION_COUNT   :  integer := 1;
  constant C_UCDB_ACTION_IGNORE  :  integer := 0;
  constant C_UCDB_ACTION_ILLEGAL :  integer := -1;

  type t_ucdb_range_array_type is array (integer range <>) of t_ucdb_range_type;

  --  Create Initial Data Structure for Point/Item Functional Coverage Model
  --  Sets initial name of the coverage model if available
  --  This procedure is used by fli_create_ucdb_coverpoint function
  procedure fli_create_ucdb_coverpoint( obj: OUT t_ucdb_cp_handle; name: IN string );

  --  Sets/Updates the name of the Coverage Model.
  --  Should not be called until the data structure is created by fli_create_ucdb_coverpoint or VendorCovCrossCreate.
  --  Replaces name that was set by fli_create_ucdb_coverpoint or VendorCovCrossCreate.
  procedure fli_set_ucdb_coverpoint_name( obj: t_ucdb_cp_handle; name: string );

  --  Add a bin or set of bins to either a Point/Item or Cross Functional Coverage Model
  --  Checking for sizing that is different from original sizing already done in OSVVM CoveragePkg
  --  It is important to maintain an index that corresponds to the order the bins were entered as 
  --  that is used when coverage is recorded.
  procedure fli_add_ucdb_bin( obj: t_ucdb_cp_handle; Action: integer; atleast: integer; name: string; index: OUT t_ucdb_bin_index );

  --  Increment the coverage of bin identified by index number.
  --  Index ranges from 1 to Number of Bins.  
  --  Index corresponds to the order the bins were entered (starting from 1)
  procedure fli_increment_ucdb_bin( obj: t_ucdb_cp_handle; index: integer );

end package vendor_func_cov_extension_pkg;

package body vendor_func_cov_extension_pkg is

  function vendor_create_coverpoint_var  return integer is
  begin
    return 0;
  end;

  procedure vendor_func_cov_set_sampling_var (id: integer; path: string) is
  begin
  end;

  procedure vendor_func_cov_set_coverpoint_var (id: integer; path: string) is
  begin
  end;

  procedure vendor_func_cov_sample_coverage (id: integer) is
  begin
  end;

  procedure vendor_func_cov_add_bin (id: integer; name: string; kind: integer; isTran: integer; lval: integer; rval: integer) is
  begin
  end;

  procedure vendor_func_cov_bin_add_value (id: integer; lval: integer; rval: integer) is
  begin
  end;

  function vendor_func_cov_get_bin_hits(id: integer; name: string)  return integer is
  begin
    return 0;
  end;

  procedure vendor_func_cov_clear_coverage (id: integer) is
  begin
  end;

  --  Create Initial Data Structure for Point/Item Functional Coverage Model
  --  Sets initial name of the coverage model if available
  --  This procedure is used by fli_create_ucdb_coverpoint function
  procedure fli_create_ucdb_coverpoint( obj: OUT t_ucdb_cp_handle; name: IN string )  is
  begin
  end procedure fli_create_ucdb_coverpoint;

  --  Sets/Updates the name of the Coverage Model.
  --  Should not be called until the data structure is created by fli_create_ucdb_coverpoint or VendorCovCrossCreate.
  --  Replaces name that was set by fli_create_ucdb_coverpoint or VendorCovCrossCreate.
  procedure fli_set_ucdb_coverpoint_name( obj: t_ucdb_cp_handle; name: string ) is
  begin
  end procedure fli_set_ucdb_coverpoint_name;

  --  Add a bin or set of bins to either a Point/Item or Cross Functional Coverage Model
  --  Checking for sizing that is different from original sizing already done in OSVVM CoveragePkg
  --  It is important to maintain an index that corresponds to the order the bins were entered as 
  --  that is used when coverage is recorded.
  procedure fli_add_ucdb_bin( obj: t_ucdb_cp_handle; Action: integer; atleast: integer; name: string; index: OUT t_ucdb_bin_index )is
  begin
  end procedure fli_add_ucdb_bin;

  --  Increment the coverage of bin identified by index number.
  --  Index ranges from 1 to Number of Bins.
  --  Index corresponds to the order the bins were entered (starting from 1)
  procedure fli_increment_ucdb_bin( obj: t_ucdb_cp_handle; index: integer )is
  begin
  end procedure fli_increment_ucdb_bin;

end package body vendor_func_cov_extension_pkg;
