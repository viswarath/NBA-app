import * as React from 'react';
import { GridColDef } from '@mui/x-data-grid';
import { DataTable } from '../DefaultTable';  // Import the abstracted DataTable component

interface TeamData {
  team_id: string;
  name: string;
  rank: number;
  wins: number;
  losses: number;
}

const teamColumns: GridColDef[] = [
  { field: 'team_id', headerName: 'Team ID', width: 150 },
  { field: 'name', headerName: 'Team Name', width: 200 },
  { field: 'rank', headerName: 'Rank', width: 150 },
  { field: 'wins', headerName: 'Wins', width: 150 },
  { field: 'losses', headerName: 'Losses', width: 150 },
];

const fetchTeams = async (name: string) => {
  const response = await fetch(`http://0.0.0.0:8000/teams?name=${name}`);
  if (!response.ok) {
    throw new Error('Error fetching data');
  }
  return response.json();
};

export const TeamDataTable: React.FC = () => {
  return (
    <DataTable<TeamData>
      queryKey={['teams']}
      queryFn={fetchTeams}
      columns={teamColumns}
      label="Team Name"
      getRowId={(row) => row.team_id}
    />
  );
};
