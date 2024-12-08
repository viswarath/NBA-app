import { Stack } from '@mui/material';
import React from 'react'
import { TeamDataTable } from '../tables/TeamTables/TeamTable';
import { SpecializedTeamTable } from '../tables/TeamTables/SpecializedTeamTable';

export const TeamPage : React.FC = () => {
    return(
        <Stack spacing={3}>
            <TeamDataTable/>
            <SpecializedTeamTable/>
        </Stack>
    );
}