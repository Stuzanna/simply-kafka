
# Topics

## Customers

{
    key: internet uuid,
    value:
        profile
            name
            job_title
            blood_group
            creditCardNumber
            address
            contact
                email
                phone
    config: throttle = 5 seconds
}

## Customers masked

Customers, masked by interceptor config, see [inteceptors.json](./interceptors.json).

## Customers encrypted

Customers, encrypted by interceptor config, see [inteceptors.json](./interceptors.json).

## Products

{
    key: internet uuid,
    value:
        name
        color
        price
    config: throttle = 2 seconds
}

## Purchases

{
    key: internet uuid,
    value:
        customerId
        productId
        timestamp
        quantity
    config: throttle = 12 seconds
}

## Returns

{
    key: internet uuid,
    value:
        customerId
        purchaseId
        timestamp
        reason: lorem.paragraph
    config: throttle = 6 seconds
}