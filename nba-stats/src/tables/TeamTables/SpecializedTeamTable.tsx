import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Button, Stack, Paper, Alert, Skeleton, TextField } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

interface SpecializedTeamData {
  team_id: number;
  name: string;
  rank: string;
  wins: number;
  losses: number;
  awards?: number;  
  SOS?: number;     
  num_road_games?: number; 
}

export const SpecializedTeamTable: React.FC = () => {
  const [filterType, setFilterType] = useState<'Team Awards' | 'Team SOS' | 'Road Games' | null>(null);
  const [SOSValue, setSOSValue] = useState<number | null>(null); 
  
  const { isLoading, isError, data, error } = useQuery<SpecializedTeamData[], Error>({
    queryKey: ['teams', filterType, SOSValue],
    queryFn: async () => {
      if (!filterType) return [];

      let url = '';
      switch (filterType) {
        case 'Team Awards':
          url = `http://0.0.0.0:8000/teamAwards`;
          break;
        case 'Team SOS':
          if (SOSValue !== null) {
            url = `http://0.0.0.0:8000/teamSOS?SOS=${SOSValue}`;
          } else {
            throw new Error('SOS value must be provided');
          }
          break;
        case 'Road Games':
          url = `http://0.0.0.0:8000/roadgames`;
          break;
        default:
          throw new Error('Invalid filter type');
      }

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Error fetching data');
      }
      return response.json();
    },
    retry: 1,
    enabled: filterType !== null && (filterType !== 'Team SOS' || SOSValue !== null), 
  });

  const handleFilterClick = (type: 'Team Awards' | 'Team SOS' | 'Road Games') => {
    setFilterType(type);
    if (type === 'Team SOS') {
      setSOSValue(null); 
    }
  };

  const handleSOSValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSOSValue(Number(event.target.value));
  };

  const columns: GridColDef[] = [
    { field: 'team_id', headerName: 'Team ID', width: 150 },
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'rank', headerName: 'Rank', width: 150 },
    { field: 'wins', headerName: 'Wins', width: 150 },
    { field: 'losses', headerName: 'Losses', width: 150 },
    {
      field: 'special_stat',
      headerName: filterType ? `${filterType.charAt(0).toUpperCase() + filterType.slice(1)}` : 'Special Stat',
      width: 150,
    },
  ];

  const rows = data?.map((team) => ({
    id: team.team_id,
    team_id: team.team_id,
    name: team.name,
    rank: team.rank,
    wins: team.wins,
    losses: team.losses,
    special_stat: 
      filterType === 'Team Awards' ? team.awards :
      filterType === 'Team SOS' ? team.SOS :
      filterType === 'Road Games' ? team.num_road_games : null,
  })) || [];

  return (
    <Stack spacing={2}>
      <Stack 
        direction="row" 
        spacing={2} 
        sx={{
         justifyContent: "center",
         alignItems: "center",
      }}>
        <Button variant="contained" onClick={() => handleFilterClick('Team Awards')}>Team Awards</Button>
        <Button variant="contained" onClick={() => handleFilterClick('Team SOS')}>Team SOS</Button>
        <Button variant="contained" onClick={() => handleFilterClick('Road Games')}>Road Games</Button>
      </Stack>

      {filterType === 'Team SOS' && (
        <Stack direction="row" spacing={2} sx={{ justifyContent: 'center' }}>
          <TextField
            label="Enter SOS Value"
            variant="standard"
            type="number"
            value={SOSValue ?? ''}
            onChange={handleSOSValueChange}
            fullWidth
          />
        </Stack>
      )}

      {isError && <Alert severity="error">Error: {error?.message}</Alert>}
      
      <Paper sx={{ height: 400, width: '100%' }}>
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
};
