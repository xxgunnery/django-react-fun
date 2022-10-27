import { Box, Button, Flex, VStack, SimpleGrid, GridItem, Container, Heading, Image, useColorModeValue } from '@chakra-ui/react'

import styles from "./common-components.module.css"

export default function Waiting() {
   let width= "30%"

   return (
      <Flex
         w="100%"
         h="100%"
         alignItems="center"
         justifyContent="center"
      >
         <Box
            className="centerFlex"
            minH="50px"
            bg={useColorModeValue("gray.800", "gray.300")}
            display="flex"
         >
            <Image w={width} src="/images/puff-loading.png" />
         </Box>
      </Flex>
   )
}