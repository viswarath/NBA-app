import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { Stack, TextField, Alert, Skeleton } from '@mui/material';
import { useQuery } from '@tanstack/react-query';

interface DataTableProps<T> {
  queryKey: string[];
  queryFn: (searchParam: string) => Promise<T[]>;
  columns: GridColDef[];
  label: string;
  getRowId: (row: T) => string | number;
  disabledSearch?: boolean;
  key?: number; 
}

export function DataTable<T>({
  queryKey,
  queryFn,
  columns,
  label,
  getRowId,
  disabledSearch,
  key,
}: DataTableProps<T>) {
  const [searchParam, setSearchParam] = React.useState<string>('');

  const { isLoading, isError, data, error, refetch } = useQuery<T[], Error>({
    queryKey: [queryKey, searchParam, key],
    queryFn: () => queryFn(searchParam),
    retry: 1,
  });

  React.useEffect(() => {
    // eslint-disable-next-line no-self-compare
    if (key ?? 0 > 0) {
      refetch();
    }
  }, [key, refetch]);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchParam(event.target.value);
  };

  const rows = data?.map((item: any) => ({
    id: getRowId(item),
    ...item,
  })) || [];

  return (
    <Stack spacing={2}>
      {!disabledSearch && (
        <TextField
          id="search-input"
          label={label}
          variant="standard"
          fullWidth
          value={searchParam}
          onChange={handleChange}
        />
      )}

      {isError && <Alert severity="error">Error: {error?.message}</Alert>}

      <Paper sx={{ height: 600, width: '100%' }}>
        {isLoading ? (
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {[...Array(5)].map((_, index) => (
              <Skeleton key={index} variant="rectangular" height={40} sx={{ margin: '5px 0' }} />
            ))}
          </div>
        ) : (
          <DataGrid
            rows={rows}
            columns={columns}
            loading={isLoading}
            getRowId={(row) => row.id}
          />
        )}
      </Paper>
    </Stack>
  );
}
