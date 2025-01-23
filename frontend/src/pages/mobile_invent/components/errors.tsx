import { Box, Button, Typography } from "@mui/material"
import axios from "axios"
import { useContext } from "react"
import { ActionContext, ItemContext, LoadingContext } from "../context"

const errors = new Map<string, string>([
        ["no ereq", "one"],
        ["no iterq", "two"]
])


type props = {
        error: string;
}

export default function Error({ error }: props) {
        const [_loading, setLoading] = useContext(LoadingContext);
        const [item, _setItem] = useContext(ItemContext);
        const [action, _setAction] = useContext(ActionContext);


        const handelSend = () => {
                setLoading(true)
                axios.post('', { action: action, item: JSON.stringify(item) })
                        .then()
                        .finally(() => setLoading(false))
        }


        return (
                <Box>
                        <Typography>
                                {errors.get(error)}
                        </Typography>
                        <Button onClick={() => handelSend()}>
                                Сообщить о проблема
                        </Button>
                </Box>
        )

}
