import TextField from '@mui/material/TextField';



export default function SearchBar() {
        const label = "Введите запрос"
        return (
                <TextField id="search-bar" label={label} fullWidth />
        )
}
