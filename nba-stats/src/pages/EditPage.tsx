import React, { useState } from 'react';
import { Stack, TextField, Button, Typography, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import { useQuery, useMutation } from '@tanstack/react-query';

const EditPage: React.FC = () => {
    const [playerId, setPlayerId] = useState<number>(0);
    const [teamId, setTeamId] = useState<string>('');
    const [name, setName] = useState<string>('');
    const [age, setAge] = useState<number>(0);
    const [position, setPosition] = useState<string>('');
    const [gamesStarted, setGamesStarted] = useState<number>(0);
    const [message, setMessage] = useState<string>('');

    const { data: players, isLoading, error } = useQuery({
        queryKey: ['players'], 
        queryFn: async () => {
            const response = await fetch('http://0.0.0.0:8000/players');
            return response.json();
        }
    });

    const { mutate: insertPlayerMutation, isPending: isInserting } = useMutation({
        mutationKey: ['insertPlayer'],
        mutationFn: async () => {
            const response = await fetch('http://0.0.0.0:8000/insertPlayer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ team_id: teamId, name, age, position, games_started: gamesStarted }),
            });
    
            if (!response.ok) {
                const errorBody = await response.json().catch(() => response.text());
                const errorMessage = errorBody.detail || 'Error inserting player';
                throw new Error(errorMessage);
            }
    
            return response.json();
        },
        onSuccess: (data) => setMessage(`Player inserted successfully: ${JSON.stringify(data)}`),
        onError: (error) => setMessage(`${error.message}`),
    });
    

    const { mutate: updatePlayerMutation, isPending: isUpdating } = useMutation({
        mutationKey: ['updatePlayer'],
        mutationFn: async () => {
            const response = await fetch('http://0.0.0.0:8000/updatePlayer', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player_id: playerId, team_id: teamId, name, age, position, games_started: gamesStarted }),
            });
    
            if (!response.ok) {
                const errorBody = await response.json().catch(() => response.text());
                const errorMessage = errorBody.detail || 'Error updating player';
                throw new Error(errorMessage);
            }
    
            return response.json();
        },
        onSuccess: (data) => setMessage(`Player updated successfully: ${JSON.stringify(data)}`),
        onError: (error) => setMessage(`${error.message}`),
    });
    

    const { mutate: deletePlayerMutation, isPending: isDeleting } = useMutation({
        mutationKey: ['deletePlayer'],
        mutationFn: async () => {
            const response = await fetch('http://0.0.0.0:8000/deletePlayer', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player_id: playerId }),
            });
            if (!response.ok) throw new Error('Error deleting player');
            return response.json();
    },
        onSuccess: (data) => setMessage(`Player deleted successfully: ${JSON.stringify(data)}`),
        onError: (error) => setMessage(`Error: ${error.message}`),
    });

    const handleInsertPlayer = () => insertPlayerMutation();
    const handleUpdatePlayer = () => updatePlayerMutation();
    const handleDeletePlayer = () => deletePlayerMutation();

    const handlePlayerSelect = (player: any) => {
    setPlayerId(player.player_id);
    setTeamId(player.team_id);
    setName(player.name);
    setAge(player.age);
    setPosition(player.position);
    setGamesStarted(player.games_started);
    };

    if (isLoading) return <Typography>Loading players...</Typography>;
    if (error) return <Typography color="error">Error fetching players: {String(error)}</Typography>;

    return (
        <Stack spacing={3} sx={{ width: '400px', margin: 'auto', paddingTop: '20px' }}>
            <Typography variant="h5">Edit Player</Typography>
            <FormControl fullWidth variant="outlined">
                <InputLabel id="select-player-label">Select Player</InputLabel>
                <Select 
                    labelId="select-player-label" 
                    value={playerId || ''} 
                    label="Select Player" 
                    onChange={(e) => handlePlayerSelect(players.find((player: any) => player.player_id === e.target.value))}
                >
                    {players.map((player: any) => (
                        <MenuItem key={player.player_id} value={player.player_id}>
                            {player.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <TextField 
                label="Team ID" 
                value={teamId} 
                onChange={(e) => setTeamId(e.target.value)} 
                fullWidth 
                variant="outlined" 
            />
            <TextField 
                label="Name" 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                fullWidth 
                variant="outlined" 
            />
            <TextField 
                label="Age" 
                type="number" 
                value={age} 
                onChange={(e) => setAge(Number(e.target.value))} 
                fullWidth 
                variant="outlined" 
            />
            <TextField 
                label="Position" 
                value={position} 
                onChange={(e) => setPosition(e.target.value)} 
                fullWidth 
                variant="outlined" 
            />
            <TextField 
                label="Games Started" 
                type="number" 
                value={gamesStarted} 
                onChange={(e) => setGamesStarted(Number(e.target.value))} 
                fullWidth 
                variant="outlined" 
            />
            <Stack direction="row" spacing={2}>
                <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleInsertPlayer} 
                    disabled={isInserting}
                >
                    {isInserting ? 'Inserting...' : 'Insert Player'}
                </Button>
                <Button 
                    variant="contained" 
                    color="secondary" 
                    onClick={handleUpdatePlayer} 
                    disabled={isUpdating}
                >
                    {isUpdating ? 'Updating...' : 'Update Player'}
                </Button>
                <Button 
                    variant="contained" 
                    color="error" 
                    onClick={handleDeletePlayer} 
                    disabled={isDeleting}
                >
                    {isDeleting ? 'Deleting...' : 'Delete Player'}
                </Button>
            </Stack>
            {message && <Typography variant="body2" color="textSecondary">{message}</Typography>}
        </Stack>
    );    
};

export default EditPage;
