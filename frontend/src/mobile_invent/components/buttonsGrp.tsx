import { useEffect, useState } from "react";
import Grid from "@mui/material/Grid2";

import Button from '@mui/material/Button';
import { Item } from "../datatypes";

const actionMap = new Map([['takeback', "Сдать"], ["giveaway", "Выдать"]])

type props = {
        action: string;
        item: Item
}

export default function ButtonGroup({ action }: props) {
        const [actionText, setActionText] = useState<string | undefined>();
        const [blank, setBlank] = useState<File | null>(null);

        const handleDownload = () => { };

        const handleUpload = () => { };

        useEffect(() => {
                setActionText(actionMap.get(action))
        }, [])
        return (
                <Grid container>
                        <Grid>
                                <Button variant="text">Скачать бланк</Button></Grid>
                        <Grid></Grid>
                        <Grid>
                                <Button variant="contained"
                                        onClick={handleUpload}
                                        disabled={true}
                                >{actionText}</Button>
                        </Grid>
                </Grid>
        )
}
