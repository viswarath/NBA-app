import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { Stack, TextField, Alert, Skeleton, Button } from '@mui/material';
import { useQuery } from '@tanstack/react-query';

interface TeamData {
  team_id: number;
  name: string; 
  rank: number;
  wins: number;
  losses: number;
}

interface TeamStatData {
  team_id: number;
  name: string; 
  rank: number;
  wins: number;
  losses: number;
  team_stat: number;
}

// Team_stat can be a decimal when you request SOS... is it okay that it is a number in the interface