import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useState } from 'react';


export default function ActionSelect() {
        const [action, setAction] = useState<string>();

        return (
                <FormControl fullWidth>
                        <InputLabel id="action-select-label">Выберите действие</InputLabel>
                        <Select
                                labelId="action-select-label"
                                id="action-select"
                                value={action}
                                label="Выберите действие"
                                onChange={(event) => setAction(event.target.value)}>
                                <MenuItem value={"giveaway"}>Выдать по заявке</MenuItem>
                                <MenuItem value={'takeback'}>Сдать</MenuItem>
                                <MenuItem value={'send'}>Переслать</MenuItem>
                        </Select>
                </FormControl >
        )
}
